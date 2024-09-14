async function L() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function M(e) {
  return await L(), e().then((t) => t.default);
}
function A(e) {
  const {
    gradio: t,
    _internal: i,
    ...n
  } = e;
  return Object.keys(i).reduce((o, s) => {
    const r = s.match(/bind_(.+)_event/);
    if (r) {
      const u = r[1], l = u.split("_"), a = (..._) => {
        const p = _.map((c) => _ && typeof c == "object" && (c.nativeEvent || c instanceof Event) ? {
          type: c.type,
          detail: c.detail,
          timestamp: c.timeStamp,
          clientX: c.clientX,
          clientY: c.clientY,
          targetId: c.target.id,
          targetClassName: c.target.className,
          altKey: c.altKey,
          ctrlKey: c.ctrlKey,
          shiftKey: c.shiftKey,
          metaKey: c.metaKey
        } : c);
        return t.dispatch(u.replace(/[A-Z]/g, (c) => "_" + c.toLowerCase()), {
          payload: p,
          component: n
        });
      };
      if (l.length > 1) {
        let _ = {
          ...n.props[l[0]] || {}
        };
        o[l[0]] = _;
        for (let c = 1; c < l.length - 1; c++) {
          const m = {
            ...n.props[l[c]] || {}
          };
          _[l[c]] = m, _ = m;
        }
        const p = l[l.length - 1];
        return _[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = a, o;
      }
      const d = l[0];
      o[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = a;
    }
    return o;
  }, {});
}
function C() {
}
function V(e) {
  return e();
}
function Z(e) {
  e.forEach(V);
}
function H(e) {
  return typeof e == "function";
}
function J(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function R(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return C;
  }
  const i = e.subscribe(...t);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function v(e) {
  let t;
  return R(e, (i) => t = i)(), t;
}
const k = [];
function Q(e, t) {
  return {
    subscribe: y(e, t).subscribe
  };
}
function y(e, t = C) {
  let i;
  const n = /* @__PURE__ */ new Set();
  function o(u) {
    if (J(e, u) && (e = u, i)) {
      const l = !k.length;
      for (const a of n)
        a[1](), k.push(a, e);
      if (l) {
        for (let a = 0; a < k.length; a += 2)
          k[a][0](k[a + 1]);
        k.length = 0;
      }
    }
  }
  function s(u) {
    o(u(e));
  }
  function r(u, l = C) {
    const a = [u, l];
    return n.add(a), n.size === 1 && (i = t(o, s) || C), u(e), () => {
      n.delete(a), n.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
    update: s,
    subscribe: r
  };
}
function je(e, t, i) {
  const n = !Array.isArray(e), o = n ? [e] : e;
  if (!o.every(Boolean))
    throw new Error("derived() expects stores as input, got a falsy value");
  const s = t.length < 2;
  return Q(i, (r, u) => {
    let l = !1;
    const a = [];
    let d = 0, _ = C;
    const p = () => {
      if (d)
        return;
      _();
      const m = t(n ? a[0] : a, r, u);
      s ? r(m) : _ = H(m) ? m : C;
    }, c = o.map((m, h) => R(m, (w) => {
      a[h] = w, d &= ~(1 << h), l && p();
    }, () => {
      d |= 1 << h;
    }));
    return l = !0, p(), function() {
      Z(c), _(), l = !1;
    };
  });
}
const {
  getContext: j,
  setContext: E
} = window.__gradio__svelte__internal, T = "$$ms-gr-antd-slots-key";
function W() {
  const e = y({});
  return E(T, e);
}
const $ = "$$ms-gr-antd-context-key";
function ee(e) {
  var u;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = ne(), i = se({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((l) => {
    i.slotKey.set(l);
  }), te();
  const n = j($), o = ((u = v(n)) == null ? void 0 : u.as_item) || e.as_item, s = n ? o ? v(n)[o] : v(n) : {}, r = y({
    ...e,
    ...s
  });
  return n ? (n.subscribe((l) => {
    const {
      as_item: a
    } = v(r);
    a && (l = l[a]), r.update((d) => ({
      ...d,
      ...l
    }));
  }), [r, (l) => {
    const a = l.as_item ? v(n)[l.as_item] : v(n);
    return r.set({
      ...l,
      ...a
    });
  }]) : [r, (l) => {
    r.set(l);
  }];
}
const U = "$$ms-gr-antd-slot-key";
function te() {
  E(U, y(void 0));
}
function ne() {
  return j(U);
}
const X = "$$ms-gr-antd-component-slot-context-key";
function se({
  slot: e,
  index: t,
  subIndex: i
}) {
  return E(X, {
    slotKey: y(e),
    slotIndex: y(t),
    subSlotIndex: y(i)
  });
}
function Ee() {
  return j(X);
}
function oe(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var Y = {
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
    function i() {
      for (var s = "", r = 0; r < arguments.length; r++) {
        var u = arguments[r];
        u && (s = o(s, n(u)));
      }
      return s;
    }
    function n(s) {
      if (typeof s == "string" || typeof s == "number")
        return s;
      if (typeof s != "object")
        return "";
      if (Array.isArray(s))
        return i.apply(null, s);
      if (s.toString !== Object.prototype.toString && !s.toString.toString().includes("[native code]"))
        return s.toString();
      var r = "";
      for (var u in s)
        t.call(s, u) && s[u] && (r = o(r, u));
      return r;
    }
    function o(s, r) {
      return r ? s ? s + " " + r : s + r : s;
    }
    e.exports ? (i.default = i, e.exports = i) : window.classNames = i;
  })();
})(Y);
var ie = Y.exports;
const I = /* @__PURE__ */ oe(ie), {
  SvelteComponent: re,
  assign: le,
  check_outros: ce,
  component_subscribe: x,
  create_component: ue,
  create_slot: ae,
  destroy_component: fe,
  detach: B,
  empty: D,
  flush: g,
  get_all_dirty_from_scope: _e,
  get_slot_changes: me,
  get_spread_object: O,
  get_spread_update: de,
  group_outros: pe,
  handle_promise: be,
  init: he,
  insert: F,
  mount_component: ge,
  noop: b,
  safe_not_equal: ye,
  transition_in: K,
  transition_out: S,
  update_await_block_branch: we,
  update_slot_base: ve
} = window.__gradio__svelte__internal;
function q(e) {
  let t, i, n = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Se,
    then: Ce,
    catch: ke,
    value: 18,
    blocks: [, , ,]
  };
  return be(
    /*AwaitedAvatarGroup*/
    e[2],
    n
  ), {
    c() {
      t = D(), n.block.c();
    },
    m(o, s) {
      F(o, t, s), n.block.m(o, n.anchor = s), n.mount = () => t.parentNode, n.anchor = t, i = !0;
    },
    p(o, s) {
      e = o, we(n, e, s);
    },
    i(o) {
      i || (K(n.block), i = !0);
    },
    o(o) {
      for (let s = 0; s < 3; s += 1) {
        const r = n.blocks[s];
        S(r);
      }
      i = !1;
    },
    d(o) {
      o && B(t), n.block.d(o), n.token = null, n = null;
    }
  };
}
function ke(e) {
  return {
    c: b,
    m: b,
    p: b,
    i: b,
    o: b,
    d: b
  };
}
function Ce(e) {
  let t, i;
  const n = [
    {
      style: (
        /*$mergedProps*/
        e[0].elem_style
      )
    },
    {
      className: I(
        /*$mergedProps*/
        e[0].elem_classes,
        "ms-gr-antd-avatar-group"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[0].elem_id
      )
    },
    /*$mergedProps*/
    e[0].props,
    A(
      /*$mergedProps*/
      e[0]
    ),
    {
      slots: (
        /*$slots*/
        e[1]
      )
    }
  ];
  let o = {
    $$slots: {
      default: [Ke]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let s = 0; s < n.length; s += 1)
    o = le(o, n[s]);
  return t = new /*AvatarGroup*/
  e[18]({
    props: o
  }), {
    c() {
      ue(t.$$.fragment);
    },
    m(s, r) {
      ge(t, s, r), i = !0;
    },
    p(s, r) {
      const u = r & /*$mergedProps, $slots*/
      3 ? de(n, [r & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          s[0].elem_style
        )
      }, r & /*$mergedProps*/
      1 && {
        className: I(
          /*$mergedProps*/
          s[0].elem_classes,
          "ms-gr-antd-avatar-group"
        )
      }, r & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          s[0].elem_id
        )
      }, r & /*$mergedProps*/
      1 && O(
        /*$mergedProps*/
        s[0].props
      ), r & /*$mergedProps*/
      1 && O(A(
        /*$mergedProps*/
        s[0]
      )), r & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          s[1]
        )
      }]) : {};
      r & /*$$scope*/
      65536 && (u.$$scope = {
        dirty: r,
        ctx: s
      }), t.$set(u);
    },
    i(s) {
      i || (K(t.$$.fragment, s), i = !0);
    },
    o(s) {
      S(t.$$.fragment, s), i = !1;
    },
    d(s) {
      fe(t, s);
    }
  };
}
function Ke(e) {
  let t;
  const i = (
    /*#slots*/
    e[15].default
  ), n = ae(
    i,
    e,
    /*$$scope*/
    e[16],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(o, s) {
      n && n.m(o, s), t = !0;
    },
    p(o, s) {
      n && n.p && (!t || s & /*$$scope*/
      65536) && ve(
        n,
        i,
        o,
        /*$$scope*/
        o[16],
        t ? me(
          i,
          /*$$scope*/
          o[16],
          s,
          null
        ) : _e(
          /*$$scope*/
          o[16]
        ),
        null
      );
    },
    i(o) {
      t || (K(n, o), t = !0);
    },
    o(o) {
      S(n, o), t = !1;
    },
    d(o) {
      n && n.d(o);
    }
  };
}
function Se(e) {
  return {
    c: b,
    m: b,
    p: b,
    i: b,
    o: b,
    d: b
  };
}
function Pe(e) {
  let t, i, n = (
    /*$mergedProps*/
    e[0].visible && q(e)
  );
  return {
    c() {
      n && n.c(), t = D();
    },
    m(o, s) {
      n && n.m(o, s), F(o, t, s), i = !0;
    },
    p(o, [s]) {
      /*$mergedProps*/
      o[0].visible ? n ? (n.p(o, s), s & /*$mergedProps*/
      1 && K(n, 1)) : (n = q(o), n.c(), K(n, 1), n.m(t.parentNode, t)) : n && (pe(), S(n, 1, 1, () => {
        n = null;
      }), ce());
    },
    i(o) {
      i || (K(n), i = !0);
    },
    o(o) {
      S(n), i = !1;
    },
    d(o) {
      o && B(t), n && n.d(o);
    }
  };
}
function xe(e, t, i) {
  let n, o, s, {
    $$slots: r = {},
    $$scope: u
  } = t;
  const l = M(() => import("./avatar.group-DbLJVFqB.js"));
  let {
    gradio: a
  } = t, {
    props: d = {}
  } = t;
  const _ = y(d);
  x(e, _, (f) => i(14, n = f));
  let {
    _internal: p = {}
  } = t, {
    as_item: c
  } = t, {
    visible: m = !0
  } = t, {
    elem_id: h = ""
  } = t, {
    elem_classes: w = []
  } = t, {
    elem_style: P = {}
  } = t;
  const [N, G] = ee({
    gradio: a,
    props: n,
    _internal: p,
    visible: m,
    elem_id: h,
    elem_classes: w,
    elem_style: P,
    as_item: c
  });
  x(e, N, (f) => i(0, o = f));
  const z = W();
  return x(e, z, (f) => i(1, s = f)), e.$$set = (f) => {
    "gradio" in f && i(6, a = f.gradio), "props" in f && i(7, d = f.props), "_internal" in f && i(8, p = f._internal), "as_item" in f && i(9, c = f.as_item), "visible" in f && i(10, m = f.visible), "elem_id" in f && i(11, h = f.elem_id), "elem_classes" in f && i(12, w = f.elem_classes), "elem_style" in f && i(13, P = f.elem_style), "$$scope" in f && i(16, u = f.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    128 && _.update((f) => ({
      ...f,
      ...d
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item*/
    32576 && G({
      gradio: a,
      props: n,
      _internal: p,
      visible: m,
      elem_id: h,
      elem_classes: w,
      elem_style: P,
      as_item: c
    });
  }, [o, s, l, _, N, z, a, d, p, c, m, h, w, P, n, r, u];
}
class Ne extends re {
  constructor(t) {
    super(), he(this, t, xe, Pe, ye, {
      gradio: 6,
      props: 7,
      _internal: 8,
      as_item: 9,
      visible: 10,
      elem_id: 11,
      elem_classes: 12,
      elem_style: 13
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), g();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(t) {
    this.$$set({
      props: t
    }), g();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), g();
  }
  get as_item() {
    return this.$$.ctx[9];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), g();
  }
  get visible() {
    return this.$$.ctx[10];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), g();
  }
  get elem_id() {
    return this.$$.ctx[11];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), g();
  }
  get elem_classes() {
    return this.$$.ctx[12];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), g();
  }
  get elem_style() {
    return this.$$.ctx[13];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), g();
  }
}
export {
  Ne as I,
  v as a,
  je as d,
  Ee as g,
  y as w
};
