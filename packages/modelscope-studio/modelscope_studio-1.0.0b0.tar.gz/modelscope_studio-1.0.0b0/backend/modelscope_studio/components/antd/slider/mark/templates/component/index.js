function Z(t) {
  const {
    gradio: e,
    _internal: i,
    ...l
  } = t;
  return Object.keys(i).reduce((s, n) => {
    const o = n.match(/bind_(.+)_event/);
    if (o) {
      const u = o[1], c = u.split("_"), a = (...m) => {
        const y = m.map((f) => m && typeof f == "object" && (f.nativeEvent || f instanceof Event) ? {
          type: f.type,
          detail: f.detail,
          timestamp: f.timeStamp,
          clientX: f.clientX,
          clientY: f.clientY,
          targetId: f.target.id,
          targetClassName: f.target.className,
          altKey: f.altKey,
          ctrlKey: f.ctrlKey,
          shiftKey: f.shiftKey,
          metaKey: f.metaKey
        } : f);
        return e.dispatch(u.replace(/[A-Z]/g, (f) => "_" + f.toLowerCase()), {
          payload: y,
          component: l
        });
      };
      if (c.length > 1) {
        let m = {
          ...l.props[c[0]] || {}
        };
        s[c[0]] = m;
        for (let f = 1; f < c.length - 1; f++) {
          const h = {
            ...l.props[c[f]] || {}
          };
          m[c[f]] = h, m = h;
        }
        const y = c[c.length - 1];
        return m[`on${y.slice(0, 1).toUpperCase()}${y.slice(1)}`] = a, s;
      }
      const _ = c[0];
      s[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = a;
    }
    return s;
  }, {});
}
function k() {
}
function B(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function G(t, ...e) {
  if (t == null) {
    for (const l of e)
      l(void 0);
    return k;
  }
  const i = t.subscribe(...e);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function g(t) {
  let e;
  return G(t, (i) => e = i)(), e;
}
const p = [];
function b(t, e = k) {
  let i;
  const l = /* @__PURE__ */ new Set();
  function s(u) {
    if (B(t, u) && (t = u, i)) {
      const c = !p.length;
      for (const a of l)
        a[1](), p.push(a, t);
      if (c) {
        for (let a = 0; a < p.length; a += 2)
          p[a][0](p[a + 1]);
        p.length = 0;
      }
    }
  }
  function n(u) {
    s(u(t));
  }
  function o(u, c = k) {
    const a = [u, c];
    return l.add(a), l.size === 1 && (i = e(s, n) || k), u(t), () => {
      l.delete(a), l.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: s,
    update: n,
    subscribe: o
  };
}
const {
  getContext: F,
  setContext: E
} = window.__gradio__svelte__internal, H = "$$ms-gr-antd-slots-key";
function J() {
  const t = b({});
  return E(H, t);
}
const Q = "$$ms-gr-antd-context-key";
function T(t) {
  var u;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = V(), i = ee({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((c) => {
    i.slotKey.set(c);
  }), W();
  const l = F(Q), s = ((u = g(l)) == null ? void 0 : u.as_item) || t.as_item, n = l ? s ? g(l)[s] : g(l) : {}, o = b({
    ...t,
    ...n
  });
  return l ? (l.subscribe((c) => {
    const {
      as_item: a
    } = g(o);
    a && (c = c[a]), o.update((_) => ({
      ..._,
      ...c
    }));
  }), [o, (c) => {
    const a = c.as_item ? g(l)[c.as_item] : g(l);
    return o.set({
      ...c,
      ...a
    });
  }]) : [o, (c) => {
    o.set(c);
  }];
}
const M = "$$ms-gr-antd-slot-key";
function W() {
  E(M, b(void 0));
}
function V() {
  return F(M);
}
const $ = "$$ms-gr-antd-component-slot-context-key";
function ee({
  slot: t,
  index: e,
  subIndex: i
}) {
  return E($, {
    slotKey: b(t),
    slotIndex: b(e),
    subSlotIndex: b(i)
  });
}
function te(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var R = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(t) {
  (function() {
    var e = {}.hasOwnProperty;
    function i() {
      for (var n = "", o = 0; o < arguments.length; o++) {
        var u = arguments[o];
        u && (n = s(n, l(u)));
      }
      return n;
    }
    function l(n) {
      if (typeof n == "string" || typeof n == "number")
        return n;
      if (typeof n != "object")
        return "";
      if (Array.isArray(n))
        return i.apply(null, n);
      if (n.toString !== Object.prototype.toString && !n.toString.toString().includes("[native code]"))
        return n.toString();
      var o = "";
      for (var u in n)
        e.call(n, u) && n[u] && (o = s(o, u));
      return o;
    }
    function s(n, o) {
      return o ? n ? n + " " + o : n + o : n;
    }
    t.exports ? (i.default = i, t.exports = i) : window.classNames = i;
  })();
})(R);
var ne = R.exports;
const se = /* @__PURE__ */ te(ne), {
  getContext: ie,
  setContext: le
} = window.__gradio__svelte__internal;
function oe(t) {
  const e = `$$ms-gr-antd-${t}-context-key`;
  function i(s = ["default"]) {
    const n = s.reduce((o, u) => (o[u] = b([]), o), {});
    return le(e, {
      itemsMap: n,
      allowedSlots: s
    }), n;
  }
  function l() {
    const {
      itemsMap: s,
      allowedSlots: n
    } = ie(e);
    return function(o, u, c) {
      s && (o ? s[o].update((a) => {
        const _ = [...a];
        return n.includes(o) ? _[u] = c : _[u] = void 0, _;
      }) : n.includes("default") && s.default.update((a) => {
        const _ = [...a];
        return _[u] = c, _;
      }));
    };
  }
  return {
    getItems: i,
    getSetItemFn: l
  };
}
const {
  getItems: Se,
  getSetItemFn: re
} = oe("slider"), {
  SvelteComponent: ue,
  binding_callbacks: ce,
  check_outros: fe,
  component_subscribe: x,
  create_slot: ae,
  detach: U,
  element: _e,
  empty: me,
  flush: d,
  get_all_dirty_from_scope: de,
  get_slot_changes: be,
  group_outros: ye,
  init: he,
  insert: X,
  safe_not_equal: ge,
  set_custom_element_data: pe,
  transition_in: j,
  transition_out: q,
  update_slot_base: xe
} = window.__gradio__svelte__internal;
function A(t) {
  let e, i;
  const l = (
    /*#slots*/
    t[21].default
  ), s = ae(
    l,
    t,
    /*$$scope*/
    t[20],
    null
  );
  return {
    c() {
      e = _e("svelte-slot"), s && s.c(), pe(e, "class", "svelte-1y8zqvi");
    },
    m(n, o) {
      X(n, e, o), s && s.m(e, null), t[22](e), i = !0;
    },
    p(n, o) {
      s && s.p && (!i || o & /*$$scope*/
      1048576) && xe(
        s,
        l,
        n,
        /*$$scope*/
        n[20],
        i ? be(
          l,
          /*$$scope*/
          n[20],
          o,
          null
        ) : de(
          /*$$scope*/
          n[20]
        ),
        null
      );
    },
    i(n) {
      i || (j(s, n), i = !0);
    },
    o(n) {
      q(s, n), i = !1;
    },
    d(n) {
      n && U(e), s && s.d(n), t[22](null);
    }
  };
}
function Ce(t) {
  let e, i, l = (
    /*$mergedProps*/
    t[1].visible && A(t)
  );
  return {
    c() {
      l && l.c(), e = me();
    },
    m(s, n) {
      l && l.m(s, n), X(s, e, n), i = !0;
    },
    p(s, [n]) {
      /*$mergedProps*/
      s[1].visible ? l ? (l.p(s, n), n & /*$mergedProps*/
      2 && j(l, 1)) : (l = A(s), l.c(), j(l, 1), l.m(e.parentNode, e)) : l && (ye(), q(l, 1, 1, () => {
        l = null;
      }), fe());
    },
    i(s) {
      i || (j(l), i = !0);
    },
    o(s) {
      q(l), i = !1;
    },
    d(s) {
      s && U(e), l && l.d(s);
    }
  };
}
function Ke(t, e, i) {
  let l, s, n, o, u, {
    $$slots: c = {},
    $$scope: a
  } = e, {
    gradio: _
  } = e, {
    props: m = {}
  } = e;
  const y = b(m);
  x(t, y, (r) => i(19, u = r));
  let {
    _internal: f = {}
  } = e, {
    label: h
  } = e, {
    number: C
  } = e, {
    as_item: K
  } = e, {
    visible: S = !0
  } = e, {
    elem_id: w = ""
  } = e, {
    elem_classes: I = []
  } = e, {
    elem_style: v = {}
  } = e;
  const N = V();
  x(t, N, (r) => i(18, o = r));
  const [O, Y] = T({
    gradio: _,
    props: u,
    _internal: f,
    visible: S,
    elem_id: w,
    elem_classes: I,
    elem_style: v,
    as_item: K,
    label: h,
    number: C
  });
  x(t, O, (r) => i(1, s = r));
  const z = J();
  x(t, z, (r) => i(17, n = r));
  const P = b();
  x(t, P, (r) => i(0, l = r));
  const D = re();
  function L(r) {
    ce[r ? "unshift" : "push"](() => {
      l = r, P.set(l);
    });
  }
  return t.$$set = (r) => {
    "gradio" in r && i(7, _ = r.gradio), "props" in r && i(8, m = r.props), "_internal" in r && i(9, f = r._internal), "label" in r && i(10, h = r.label), "number" in r && i(11, C = r.number), "as_item" in r && i(12, K = r.as_item), "visible" in r && i(13, S = r.visible), "elem_id" in r && i(14, w = r.elem_id), "elem_classes" in r && i(15, I = r.elem_classes), "elem_style" in r && i(16, v = r.elem_style), "$$scope" in r && i(20, a = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    256 && y.update((r) => ({
      ...r,
      ...m
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, label, number*/
    654976 && Y({
      gradio: _,
      props: u,
      _internal: f,
      visible: S,
      elem_id: w,
      elem_classes: I,
      elem_style: v,
      as_item: K,
      label: h,
      number: C
    }), t.$$.dirty & /*$slotKey, $mergedProps, $slots, $slot*/
    393219 && D(o, s._internal.index || 0, {
      props: {
        style: s.elem_style,
        className: se(s.elem_classes, "ms-gr-antd-slider-mark"),
        id: s.elem_id,
        number: s.number,
        label: s.label,
        ...s.props,
        ...Z(s)
      },
      slots: {
        ...n,
        children: s._internal.layout ? l : void 0
      }
    });
  }, [l, s, y, N, O, z, P, _, m, f, h, C, K, S, w, I, v, n, o, u, a, c, L];
}
class we extends ue {
  constructor(e) {
    super(), he(this, e, Ke, Ce, ge, {
      gradio: 7,
      props: 8,
      _internal: 9,
      label: 10,
      number: 11,
      as_item: 12,
      visible: 13,
      elem_id: 14,
      elem_classes: 15,
      elem_style: 16
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), d();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(e) {
    this.$$set({
      props: e
    }), d();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), d();
  }
  get label() {
    return this.$$.ctx[10];
  }
  set label(e) {
    this.$$set({
      label: e
    }), d();
  }
  get number() {
    return this.$$.ctx[11];
  }
  set number(e) {
    this.$$set({
      number: e
    }), d();
  }
  get as_item() {
    return this.$$.ctx[12];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), d();
  }
  get visible() {
    return this.$$.ctx[13];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), d();
  }
  get elem_id() {
    return this.$$.ctx[14];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), d();
  }
  get elem_classes() {
    return this.$$.ctx[15];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), d();
  }
  get elem_style() {
    return this.$$.ctx[16];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), d();
  }
}
export {
  we as default
};
