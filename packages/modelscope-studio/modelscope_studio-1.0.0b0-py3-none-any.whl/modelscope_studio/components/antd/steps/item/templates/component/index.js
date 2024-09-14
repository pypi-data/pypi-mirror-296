function z(e) {
  const {
    gradio: t,
    _internal: o,
    ...n
  } = e;
  return Object.keys(o).reduce((s, i) => {
    const r = i.match(/bind_(.+)_event/);
    if (r) {
      const c = r[1], l = c.split("_"), f = (...m) => {
        const d = m.map((a) => m && typeof a == "object" && (a.nativeEvent || a instanceof Event) ? {
          type: a.type,
          detail: a.detail,
          timestamp: a.timeStamp,
          clientX: a.clientX,
          clientY: a.clientY,
          targetId: a.target.id,
          targetClassName: a.target.className,
          altKey: a.altKey,
          ctrlKey: a.ctrlKey,
          shiftKey: a.shiftKey,
          metaKey: a.metaKey
        } : a);
        return t.dispatch(c.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: d,
          component: n
        });
      };
      if (l.length > 1) {
        let m = {
          ...n.props[l[0]] || {}
        };
        s[l[0]] = m;
        for (let a = 1; a < l.length - 1; a++) {
          const p = {
            ...n.props[l[a]] || {}
          };
          m[l[a]] = p, m = p;
        }
        const d = l[l.length - 1];
        return m[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = f, s;
      }
      const _ = l[0];
      s[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = f;
    }
    return s;
  }, {});
}
function w() {
}
function R(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function U(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return w;
  }
  const o = e.subscribe(...t);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function h(e) {
  let t;
  return U(e, (o) => t = o)(), t;
}
const g = [];
function b(e, t = w) {
  let o;
  const n = /* @__PURE__ */ new Set();
  function s(c) {
    if (R(e, c) && (e = c, o)) {
      const l = !g.length;
      for (const f of n)
        f[1](), g.push(f, e);
      if (l) {
        for (let f = 0; f < g.length; f += 2)
          g[f][0](g[f + 1]);
        g.length = 0;
      }
    }
  }
  function i(c) {
    s(c(e));
  }
  function r(c, l = w) {
    const f = [c, l];
    return n.add(f), n.size === 1 && (o = t(s, i) || w), c(e), () => {
      n.delete(f), n.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: s,
    update: i,
    subscribe: r
  };
}
const {
  getContext: O,
  setContext: k
} = window.__gradio__svelte__internal, X = "$$ms-gr-antd-slots-key";
function Y() {
  const e = b({});
  return k(X, e);
}
const D = "$$ms-gr-antd-context-key";
function L(e) {
  var c;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = A(), o = G({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((l) => {
    o.slotKey.set(l);
  }), Z();
  const n = O(D), s = ((c = h(n)) == null ? void 0 : c.as_item) || e.as_item, i = n ? s ? h(n)[s] : h(n) : {}, r = b({
    ...e,
    ...i
  });
  return n ? (n.subscribe((l) => {
    const {
      as_item: f
    } = h(r);
    f && (l = l[f]), r.update((_) => ({
      ..._,
      ...l
    }));
  }), [r, (l) => {
    const f = l.as_item ? h(n)[l.as_item] : h(n);
    return r.set({
      ...l,
      ...f
    });
  }]) : [r, (l) => {
    r.set(l);
  }];
}
const q = "$$ms-gr-antd-slot-key";
function Z() {
  k(q, b(void 0));
}
function A() {
  return O(q);
}
const B = "$$ms-gr-antd-component-slot-context-key";
function G({
  slot: e,
  index: t,
  subIndex: o
}) {
  return k(B, {
    slotKey: b(e),
    slotIndex: b(t),
    subSlotIndex: b(o)
  });
}
function H(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var F = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function o() {
      for (var i = "", r = 0; r < arguments.length; r++) {
        var c = arguments[r];
        c && (i = s(i, n(c)));
      }
      return i;
    }
    function n(i) {
      if (typeof i == "string" || typeof i == "number")
        return i;
      if (typeof i != "object")
        return "";
      if (Array.isArray(i))
        return o.apply(null, i);
      if (i.toString !== Object.prototype.toString && !i.toString.toString().includes("[native code]"))
        return i.toString();
      var r = "";
      for (var c in i)
        t.call(i, c) && i[c] && (r = s(r, c));
      return r;
    }
    function s(i, r) {
      return r ? i ? i + " " + r : i + r : i;
    }
    e.exports ? (o.default = o, e.exports = o) : window.classNames = o;
  })();
})(F);
var J = F.exports;
const Q = /* @__PURE__ */ H(J), {
  getContext: T,
  setContext: W
} = window.__gradio__svelte__internal;
function $(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function o(s = ["default"]) {
    const i = s.reduce((r, c) => (r[c] = b([]), r), {});
    return W(t, {
      itemsMap: i,
      allowedSlots: s
    }), i;
  }
  function n() {
    const {
      itemsMap: s,
      allowedSlots: i
    } = T(t);
    return function(r, c, l) {
      s && (r ? s[r].update((f) => {
        const _ = [...f];
        return i.includes(r) ? _[c] = l : _[c] = void 0, _;
      }) : i.includes("default") && s.default.update((f) => {
        const _ = [...f];
        return _[c] = l, _;
      }));
    };
  }
  return {
    getItems: o,
    getSetItemFn: n
  };
}
const {
  getItems: yt,
  getSetItemFn: tt
} = $("steps"), {
  SvelteComponent: et,
  check_outros: nt,
  component_subscribe: S,
  create_slot: st,
  detach: it,
  empty: ot,
  flush: y,
  get_all_dirty_from_scope: rt,
  get_slot_changes: lt,
  group_outros: ct,
  init: ut,
  insert: ft,
  safe_not_equal: at,
  transition_in: I,
  transition_out: v,
  update_slot_base: _t
} = window.__gradio__svelte__internal;
function N(e) {
  let t;
  const o = (
    /*#slots*/
    e[17].default
  ), n = st(
    o,
    e,
    /*$$scope*/
    e[16],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(s, i) {
      n && n.m(s, i), t = !0;
    },
    p(s, i) {
      n && n.p && (!t || i & /*$$scope*/
      65536) && _t(
        n,
        o,
        s,
        /*$$scope*/
        s[16],
        t ? lt(
          o,
          /*$$scope*/
          s[16],
          i,
          null
        ) : rt(
          /*$$scope*/
          s[16]
        ),
        null
      );
    },
    i(s) {
      t || (I(n, s), t = !0);
    },
    o(s) {
      v(n, s), t = !1;
    },
    d(s) {
      n && n.d(s);
    }
  };
}
function mt(e) {
  let t, o, n = (
    /*$mergedProps*/
    e[0].visible && N(e)
  );
  return {
    c() {
      n && n.c(), t = ot();
    },
    m(s, i) {
      n && n.m(s, i), ft(s, t, i), o = !0;
    },
    p(s, [i]) {
      /*$mergedProps*/
      s[0].visible ? n ? (n.p(s, i), i & /*$mergedProps*/
      1 && I(n, 1)) : (n = N(s), n.c(), I(n, 1), n.m(t.parentNode, t)) : n && (ct(), v(n, 1, 1, () => {
        n = null;
      }), nt());
    },
    i(s) {
      o || (I(n), o = !0);
    },
    o(s) {
      v(n), o = !1;
    },
    d(s) {
      s && it(t), n && n.d(s);
    }
  };
}
function dt(e, t, o) {
  let n, s, i, r, {
    $$slots: c = {},
    $$scope: l
  } = t, {
    gradio: f
  } = t, {
    props: _ = {}
  } = t;
  const m = b(_);
  S(e, m, (u) => o(15, r = u));
  let {
    _internal: d = {}
  } = t, {
    as_item: a
  } = t, {
    visible: p = !0
  } = t, {
    elem_id: x = ""
  } = t, {
    elem_classes: C = []
  } = t, {
    elem_style: K = {}
  } = t;
  const j = A();
  S(e, j, (u) => o(14, i = u));
  const [P, M] = L({
    gradio: f,
    props: r,
    _internal: d,
    visible: p,
    elem_id: x,
    elem_classes: C,
    elem_style: K,
    as_item: a
  });
  S(e, P, (u) => o(0, s = u));
  const E = Y();
  S(e, E, (u) => o(13, n = u));
  const V = tt();
  return e.$$set = (u) => {
    "gradio" in u && o(5, f = u.gradio), "props" in u && o(6, _ = u.props), "_internal" in u && o(7, d = u._internal), "as_item" in u && o(8, a = u.as_item), "visible" in u && o(9, p = u.visible), "elem_id" in u && o(10, x = u.elem_id), "elem_classes" in u && o(11, C = u.elem_classes), "elem_style" in u && o(12, K = u.elem_style), "$$scope" in u && o(16, l = u.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    64 && m.update((u) => ({
      ...u,
      ..._
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item*/
    40864 && M({
      gradio: f,
      props: r,
      _internal: d,
      visible: p,
      elem_id: x,
      elem_classes: C,
      elem_style: K,
      as_item: a
    }), e.$$.dirty & /*$slotKey, $mergedProps, $slots*/
    24577 && V(i, s._internal.index || 0, {
      props: {
        style: s.elem_style,
        className: Q(s.elem_classes, "ms-gr-antd-steps-item"),
        id: s.elem_id,
        ...s.props,
        ...z(s)
      },
      slots: n
    });
  }, [s, m, j, P, E, f, _, d, a, p, x, C, K, n, i, r, l, c];
}
class bt extends et {
  constructor(t) {
    super(), ut(this, t, dt, mt, at, {
      gradio: 5,
      props: 6,
      _internal: 7,
      as_item: 8,
      visible: 9,
      elem_id: 10,
      elem_classes: 11,
      elem_style: 12
    });
  }
  get gradio() {
    return this.$$.ctx[5];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), y();
  }
  get props() {
    return this.$$.ctx[6];
  }
  set props(t) {
    this.$$set({
      props: t
    }), y();
  }
  get _internal() {
    return this.$$.ctx[7];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), y();
  }
  get as_item() {
    return this.$$.ctx[8];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), y();
  }
  get visible() {
    return this.$$.ctx[9];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), y();
  }
  get elem_id() {
    return this.$$.ctx[10];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), y();
  }
  get elem_classes() {
    return this.$$.ctx[11];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), y();
  }
  get elem_style() {
    return this.$$.ctx[12];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), y();
  }
}
export {
  bt as default
};
